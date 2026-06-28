export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface RequestConfig {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
  timeout?: number;
}

class ApiClient {
  private baseUrl: string;
  private refreshPromise: Promise<boolean> | null = null;
  private maxRetries = 3;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getTokens() {
    if (typeof window === "undefined") return { access: null, refresh: null };
    return {
      access: localStorage.getItem("memex_access_token"),
      refresh: localStorage.getItem("memex_refresh_token"),
    };
  }

  private setTokens(access: string, refresh: string) {
    localStorage.setItem("memex_access_token", access);
    localStorage.setItem("memex_refresh_token", refresh);
  }

  private clearTokens() {
    localStorage.removeItem("memex_access_token");
    localStorage.removeItem("memex_refresh_token");
  }

  private async refreshTokens(): Promise<boolean> {
    const { refresh } = this.getTokens();
    if (!refresh) return false;

    if (this.refreshPromise) return this.refreshPromise;

    this.refreshPromise = (async () => {
      try {
        const res = await fetch(`${this.baseUrl}/api/v1/memex/auth/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refreshToken: refresh }),
        });

        if (!res.ok) {
          this.clearTokens();
          return false;
        }

        const data = await res.json();
        this.setTokens(data.data.accessToken, data.data.refreshToken);
        return true;
      } catch {
        this.clearTokens();
        return false;
      } finally {
        this.refreshPromise = null;
      }
    })();

    return this.refreshPromise;
  }

  private logError(method: string, path: string, error: unknown) {
    if (typeof console !== "undefined") {
      console.error(`[API] ${method} ${path} failed:`, error);
    }
  }

  private async sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  private shouldRetry(status: number): boolean {
    return status === 429 || status >= 500;
  }

  async request<T>(path: string, config: RequestConfig = {}, retryCount = 0): Promise<T> {
    const { access } = this.getTokens();
    const headers: Record<string, string> = {
      ...config.headers,
    };

    if (access) {
      headers.Authorization = `Bearer ${access}`;
    }

    if (config.body && !(config.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    const controller = new AbortController();
    const timeoutMs = config.timeout ?? 30000;
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const signal = config.signal
      ? anySignal([config.signal, controller.signal])
      : controller.signal;

    try {
      const res = await fetch(`${this.baseUrl}${path}`, {
        method: config.method ?? "GET",
        headers,
        body:
          config.body instanceof FormData
            ? config.body
            : config.body
              ? JSON.stringify(config.body)
              : undefined,
        signal,
      });

      clearTimeout(timeoutId);

      if (res.status === 401 && this.getTokens().refresh) {
        const refreshed = await this.refreshTokens();
        if (refreshed) {
          return this.request<T>(path, config, retryCount);
        }
      }

      if (!res.ok) {
        if (this.shouldRetry(res.status) && retryCount < this.maxRetries) {
          const delay = Math.min(1000 * 2 ** retryCount, 10000);
          this.logError(
            config.method ?? "GET",
            path,
            `Retry ${retryCount + 1}/${this.maxRetries} after ${delay}ms (status ${res.status})`,
          );
          await this.sleep(delay);
          return this.request<T>(path, config, retryCount + 1);
        }

        const error = await res.json().catch(() => ({
          error: { code: "UNKNOWN", message: res.statusText },
        }));
        throw new ApiError(
          res.status,
          error.error?.code ?? "UNKNOWN",
          error.error?.message ?? "An error occurred",
          error.error?.details,
        );
      }

      if (res.headers.get("content-type")?.includes("text/event-stream")) {
        return res as unknown as T;
      }

      const json = await res.json();
      return ("data" in json ? json.data : json) as T;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof ApiError) throw error;
      if (
        retryCount < this.maxRetries &&
        !(error instanceof DOMException && error.name === "AbortError")
      ) {
        const delay = Math.min(1000 * 2 ** retryCount, 10000);
        this.logError(
          config.method ?? "GET",
          path,
          `Network retry ${retryCount + 1}/${this.maxRetries} after ${delay}ms`,
        );
        await this.sleep(delay);
        return this.request<T>(path, config, retryCount + 1);
      }
      this.logError(config.method ?? "GET", path, error);
      throw new ApiError(
        0,
        "NETWORK_ERROR",
        error instanceof Error ? error.message : "Network error",
      );
    }
  }

  get<T>(path: string, config?: RequestConfig) {
    return this.request<T>(path, { ...config, method: "GET" });
  }

  post<T>(path: string, body?: unknown, config?: RequestConfig) {
    return this.request<T>(path, { ...config, method: "POST", body });
  }

  patch<T>(path: string, body?: unknown, config?: RequestConfig) {
    return this.request<T>(path, { ...config, method: "PATCH", body });
  }

  delete<T>(path: string, config?: RequestConfig) {
    return this.request<T>(path, { ...config, method: "DELETE" });
  }

  stream(path: string, body: unknown, signal: AbortSignal): Promise<Response> {
    const { access } = this.getTokens();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (access) {
      headers.Authorization = `Bearer ${access}`;
    }

    return fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      signal,
    });
  }
}

function anySignal(signals: AbortSignal[]): AbortSignal {
  const controller = new AbortController();

  for (const signal of signals) {
    if (signal.aborted) {
      controller.abort(signal.reason);
      return controller.signal;
    }
    signal.addEventListener("abort", () => controller.abort(signal.reason), {
      once: true,
    });
  }

  return controller.signal;
}

const apiUrl = (
  typeof window !== "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000")
    : (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000")
) as string;

export const api = new ApiClient(apiUrl);
