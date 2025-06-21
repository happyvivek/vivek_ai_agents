from crewai import Crew
from crewai.agent import Agent
from crewai.task import Task
from crewai.process import Process
from crewai.project import CrewBase, agent, task, crew

from .tools.custom_tool import (
    KubectlTool,
    RemediationTool,
    ObservabilityTool,
    SecurityAuditTool,
    CostOptimizationTool,
    UpgradeTool
)

@CrewBase
class OkeDiagnosticAgent:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def diagnostic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['diagnostic_agent'],
            tools=[KubectlTool()],
            verbose=True
        )

    @agent
    def remediation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['remediation_agent'],
            tools=[RemediationTool()],
            verbose=True
        )

    @agent
    def observability_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['observability_agent'],
            tools=[ObservabilityTool()],
            verbose=True
        )

    @agent
    def security_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['security_agent'],
            tools=[SecurityAuditTool()],
            verbose=True
        )

    @agent
    def cost_analysis_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cost_analysis_agent'],
            tools=[CostOptimizationTool()],
            verbose=True
        )

    @agent
    def upgrade_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['upgrade_agent'],
            tools=[UpgradeTool()],
            verbose=True
        )

    @task
    def diagnostic_task(self) -> Task:
        return Task(
            config=self.tasks_config['diagnostic_task'],
            agent=self.diagnostic_agent()
        )

    @task
    def remediation_task(self) -> Task:
        return Task(
            config=self.tasks_config['remediation_task'],
            agent=self.remediation_agent()
        )

    @task
    def observability_task(self) -> Task:
        return Task(
            config=self.tasks_config['observability_task'],
            agent=self.observability_agent()
        )

    @task
    def security_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_audit_task'],
            agent=self.security_agent()
        )

    @task
    def cost_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['cost_optimization_task'],
            agent=self.cost_analysis_agent()
        )

    @task
    def upgrade_readiness_task(self) -> Task:
        return Task(
            config=self.tasks_config['upgrade_readiness_task'],
            agent=self.upgrade_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
