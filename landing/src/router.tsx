import { createRouter } from "@tanstack/react-router";

import { routerBasepath } from "./lib/site-config";
import { routeTree } from "./routeTree.gen";

export const router = createRouter({
  routeTree,
  basepath: routerBasepath(),
  scrollRestoration: true,
  defaultPreloadStaleTime: 0,
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
