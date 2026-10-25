(function () {
  'use strict';
  var path=location.pathname;
  var supported=/^\/(?:c|s)\/[a-f0-9-]{36}\/$/i.test(path) || /^\/scenes\/[a-z0-9-]+\/$/.test(path) || /^\/campaign\/[a-z0-9-]+\/day\/(?:[1-9]|[12][0-9]|30)\/$/.test(path);
  if(!supported || !/Android/i.test(navigator.userAgent)) return;
  var host=document.querySelector('.share-actions') || document.querySelector('main');
  if(!host) return;
  var link=document.createElement('a');
  link.className='btn btn-primary app-open';
  link.textContent='Open in Edifice';
  link.href='intent://edificeapp.org'+path+'#Intent;scheme=https;package=com.edifice.app;S.browser_fallback_url='+encodeURIComponent('https://edificeapp.org/download/')+';end';
  host.appendChild(link);
})();
