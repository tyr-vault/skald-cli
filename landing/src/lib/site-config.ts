/** TanStack Router basepath (no trailing slash). Empty string when hosted at domain root. */
export function routerBasepath(): string {
  const base = import.meta.env.BASE_URL ?? "/";
  if (base === "/") return "";
  return base.replace(/\/$/, "");
}

/** GitHub tree or repo URL for the CLI project (override in CI or `.env`). */
export const toolRepoUrl =
  import.meta.env.VITE_TOOL_REPO_URL ?? "https://github.com/rdvid/skald";

/** Full README on GitHub for the Skald CLI. */
export const toolReadmeUrl =
  import.meta.env.VITE_TOOL_README_URL ?? `${toolRepoUrl}/blob/master/README.md`;
