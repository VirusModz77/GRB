(() => {
  const inicio = Date.now();
  let enviado = false;

  function enviar() {
    if (enviado) return;
    enviado = true;
    navigator.sendBeacon("/api/track", JSON.stringify({
      seconds: Math.round((Date.now() - inicio) / 1000),
      path: location.pathname + location.search,
      referrer: document.referrer
    }));
  }

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") enviar();
  });
})();