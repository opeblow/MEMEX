import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_ROUTES = [
  "/",
  "/login",
  "/register",
  "/verify-email",
  "/reset-password",
  "/api",
  "/_next",
  "/favicon",
];

const AUTH_ONLY_ROUTES = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isPublic = PUBLIC_ROUTES.some((route) => pathname.startsWith(route));
  const isAuthOnly = AUTH_ONLY_ROUTES.some((route) => pathname === route);

  const accessToken = request.cookies.get("memex_access_token")?.value;
  const refreshToken = request.cookies.get("memex_refresh_token")?.value;
  const isAuthenticated = !!(accessToken || refreshToken);

  if (isAuthenticated && isAuthOnly) {
    return NextResponse.redirect(new URL("/recall", request.url));
  }

  if (!isAuthenticated && !isPublic) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
