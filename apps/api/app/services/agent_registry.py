from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate


class AgentRegistryService:
    async def create_agent(
        self,
        db: AsyncSession,
        project_id: str,
        user_id: str,
        request: AgentCreate,
    ) -> Agent:
        agent = Agent(
            project_id=project_id,
            user_id=user_id,
            name=request.name,
            description=request.description,
            agent_type=request.agent_type or "custom",
            model_config=request.agent_config,
            capabilities=request.capabilities,
            memory_scope=request.memory_scope or "workspace",
            permissions=request.permissions,
            status="active",
        )
        db.add(agent)
        await db.commit()
        await db.refresh(agent)
        return agent

    async def get_agent(self, db: AsyncSession, agent_id: str) -> Agent | None:
        return await Agent.find_by_id(db, agent_id)

    async def list_agents(
        self, db: AsyncSession, project_id: str, limit: int = 50, offset: int = 0
    ) -> list[Agent]:
        return await Agent.find_by_project(db, project_id, limit, offset)

    async def update_agent(
        self, db: AsyncSession, agent_id: str, request: AgentUpdate
    ) -> Agent | None:
        agent = await Agent.find_by_id(db, agent_id)
        if not agent:
            return None
        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(agent, key, value)
        await db.commit()
        await db.refresh(agent)
        return agent

    async def delete_agent(self, db: AsyncSession, agent_id: str) -> bool:
        agent = await Agent.find_by_id(db, agent_id)
        if not agent:
            return False
        await db.delete(agent)
        await db.commit()
        return True


agent_registry_service = AgentRegistryService()
