import { getStore } from "@netlify/blobs";
import type { Context } from "@netlify/edge-functions";

export default async (request: Request, context: Context) => {
  if (request.method !== "POST") return new Response(null, { status: 405 });

  const { seconds, path, referrer } = await request.json();
  const hoy = new Date().toISOString().slice(0, 10);
  const store = getStore("analytics");

  const dia = (await store.get(hoy, { type: "json" })) ?? {};
  dia.visitas = (dia.visitas || 0) + 1;
  dia.segundosTotales = dia.segundosTotales || 0;
  dia.paises = dia.paises || {};
  dia.paginas = dia.paginas || {};
  dia.tiempoPorPagina = dia.tiempoPorPagina || {};
  dia.referrers = dia.referrers || {};

  const segs = Math.min(Math.max(seconds || 0, 0), 3600);
  dia.segundosTotales += segs;

  const [base, query] = (path || "/").split("?");
  const limpia = base.replace(/index\.html$/, "").replace(/\/+$/, "") || "/";
  const ruta = limpia + (query ? "?" + query : "");
  dia.paginas[ruta] = (dia.paginas[ruta] || 0) + 1;
  dia.tiempoPorPagina[ruta] = (dia.tiempoPorPagina[ruta] || 0) + segs;

  const pais = context.geo?.country?.name ?? "Desconocido";
  dia.paises[pais] = (dia.paises[pais] || 0) + 1;

  let ref = "directo";
  if (referrer) {
    try {
      const h = new URL(referrer).hostname;
      ref = h === new URL(request.url).hostname ? "interno" : h;
    } catch { ref = "desconocido"; }
  }
  dia.referrers[ref] = (dia.referrers[ref] || 0) + 1;

  await store.setJSON(hoy, dia);
  return new Response(null, { status: 204 });
};

export const config = { path: "/api/track" };