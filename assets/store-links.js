/*
 * Where a "get the app" control sends someone, decided per platform.
 *
 * ## Why the destinations are empty
 *
 * Neither listing is public yet — https://play.google.com/store/apps/details?id=com.edifice.app
 * answers 404 today, and there is no App Store URL at all. An empty string here means exactly
 * that, and the page keeps the state it was rendered in: a control that says the app is coming
 * rather than a link that 404s. Every page already renders that honest state in its HTML, so a
 * visitor with no JavaScript sees the same thing.
 *
 * Publishing is therefore one string each, in one file, for the whole site.
 *
 * ## What the platform detection is and is not for
 *
 * It picks which control to show, not where to send the page. Nothing here redirects. Bouncing a
 * shared link straight to a store is what App Links and Universal Links exist to avoid: someone
 * who already has Edifice would be thrown at a store page for an app they own, and someone who
 * followed the link to read something would never see it. Once /.well-known/assetlinks.json is
 * verified, a member with the app installed does not reach this page at all — the app opens.
 */
(function () {
  var STORES = {
    ios: "",
    android: ""
  };

  var ua = navigator.userAgent || "";
  var isAndroid = /Android/i.test(ua);
  // iPadOS 13+ reports itself as a Mac; the touch-point count is what separates it from a desktop.
  var isIOS = /iPad|iPhone|iPod/.test(ua) ||
    (/Macintosh/.test(ua) && (navigator.maxTouchPoints || 0) > 1);
  document.documentElement.setAttribute("data-os", isAndroid ? "android" : (isIOS ? "ios" : "other"));

  var slots = document.querySelectorAll("[data-store]");
  for (var i = 0; i < slots.length; i++) {
    var slot = slots[i];
    var href = STORES[slot.getAttribute("data-store")];
    if (!href) continue;

    var link = document.createElement("a");
    link.setAttribute("href", href);
    link.innerHTML = slot.innerHTML;
    // Every attribute, not just the class. `data-store` is what assets/site.css keys the
    // platform hide rules on, so dropping it here would leave BOTH store buttons showing on
    // both platforms — invisible today, because an empty URL means nothing is replaced at all,
    // and live the day either listing is published.
    for (var a = 0; a < slot.attributes.length; a++) {
      link.setAttribute(slot.attributes[a].name, slot.attributes[a].value);
    }
    link.removeAttribute("aria-disabled");
    link.removeAttribute("role");
    link.setAttribute("href", href);

    var label = slot.getAttribute("data-store-label");
    var labelEl = label && link.querySelector(".store-label");
    if (labelEl) labelEl.textContent = label;

    slot.parentNode.replaceChild(link, slot);
  }
})();
