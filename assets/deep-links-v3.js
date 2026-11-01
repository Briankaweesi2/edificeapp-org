(function () {
  'use strict';
  var path = location.pathname;
  var lang = document.documentElement.lang || 'en';
  var contentPath = path.replace(/^\/(?:zh|hi|es|ar)(?=\/)/, '') || '/';
  var supported = /^\/(?:c|s)\/[a-f0-9-]{36}\/$/i.test(contentPath) || /^\/scenes\/[a-z0-9-]+\/$/.test(contentPath) || /^\/campaign\/[a-z0-9-]+\/day\/(?:[1-9]|[12][0-9]|30)\/$/.test(contentPath);
  if (!supported || !/Android/i.test(navigator.userAgent)) return;
  var host = document.querySelector('.share-actions') || document.querySelector('main');
  if (!host) return;
  var link = document.createElement('a');
  link.className = 'btn btn-primary app-open';
  link.textContent = window.edificeText && window.edificeText['Open in Edifice'] || 'Open in Edifice';
  var fallback = 'https://edificeapp.org/' + (lang === 'en' ? '' : lang + '/') + 'download/';
  link.href = 'intent://edificeapp.org' + contentPath + '#Intent;scheme=https;package=com.edifice.app;S.browser_fallback_url=' + encodeURIComponent(fallback) + ';end';
  host.appendChild(link);
})();
