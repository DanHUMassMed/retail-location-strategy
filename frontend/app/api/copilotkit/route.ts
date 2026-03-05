import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";

// Use empty adapter since we're proxying to a remote AG-UI backend
const serviceAdapter = new ExperimentalEmptyAdapter();

// Use LangGraphHttpAgent with agents configuration for AG-UI protocol compatibility
// The agent name must match the app_name in the backend ADKAgent configuration
const runtime = new CopilotRuntime({
  agents: {
    retail_location_strategy: new HttpAgent({url: "http://localhost:8000/"}),
  }
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
