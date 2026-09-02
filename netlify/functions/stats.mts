import { getStore } from "@netlify/blobs";

export default async (req: Request) => {
  const token = new URL(req.url).searchParams.get("token");
  if (token !== Netlify.env.get("DASHBOARD_TOKEN")) {
    return new Response("No autorizado", { status: 401 });
  }

  const store = getStore("analytics");
  const dias = [];
  for (let i = 0; i < 14; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const clave = d.toISOString().slice(0, 10);
    const datos = await store.get(clave, { type: "json" });
    if (datos) dias.push({ fecha: clave, ...datos });
  }

  return Response.json(dias, {
    headers: { "cache-control": "no-store" },
  });
};

export const config = { path: "/api/stats" };
