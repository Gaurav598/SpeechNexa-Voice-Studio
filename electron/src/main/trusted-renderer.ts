/** Compare URL components: custom app schemes have a null URL.origin. */
export function isTrustedRenderer(raw: string, dev?: string): boolean {
  try {
    const url = new URL(raw);
    return ['app://voicestudio', ...(dev ? [dev] : [])].some((value) => {
      const allowed = new URL(value);
      const sameOrigin =
        url.protocol === allowed.protocol &&
        url.hostname === allowed.hostname &&
        url.port === allowed.port &&
        !url.username &&
        !url.password;
      if (!sameOrigin) return false;
      // Both the packaged app and dev server proxy /api to the backend. A
      // backend HTML response must never inherit the shell's preload or IPC.
      if (allowed.protocol !== 'app:') return !/^\/api(?:\/|$)/.test(url.pathname);
      return url.pathname === '/' || url.pathname === '/index.html';
    });
  } catch {
    return false;
  }
}
