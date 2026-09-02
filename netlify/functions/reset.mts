import { getStore } from "@netlify/blobs";

export default async (req: Request) => {
  const token = new URL(req.url).searchParams.get("token");
  if (token !== Netlify.env.get("DASHBOARD_TOKEN")) {
    return new Response("No autorizado", { status: 401 });
  }

  const store = getStore("analytics");
  const { blobs } = await store.list();
  for (const b of blobs) await store.delete(b.key);

  return Response.json({ borrados: blobs.length });
};

export const config = { path: "/api/reset" };