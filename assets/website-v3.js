/* First-party, opt-in measurement. No Firebase Auth/Firestore or advertising SDKs. */
(function () {
  'use strict';
  var ID = 'G-YH52011S44';
  var KEY = 'edifice-website-analytics-v1';
  var active = false;
  var production = /^(www\.)?edificeapp\.org$/.test(location.hostname);
  var saved = '';
  try { saved = localStorage.getItem(KEY) || ''; } catch (_) {}
  // Report only broad page groups, never individual confessions, stories, searches or query strings.
  var groups = ['daily-confessions', 'glory', 'download', 'about', 'themes', 'scenes', 'campaign', 'privacy', 'terms', 'support', 'delete-account'];
  var first = location.pathname.split('/')[1];
  var group = first === 'c' || first === 's' ? 'shared' : (groups.indexOf(first) >= 0 ? first : 'home');
  function start() {
    if (active || !production) return;
    active = true;
    window['ga-disable-'+ID]=false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('consent', 'update', {analytics_storage:'granted'});
    window.gtag('js', new Date());
    window.gtag('config', ID, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false, page_location:'https://edificeapp.org/'+(group==='home'?'':group+'/'), page_title:'Edifice | '+group, page_referrer:'', cookie_expires:60*60*24*90});
    window.gtag('event', 'page_view', {page_group:group});
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id='+ID;
    document.head.appendChild(script);
  }
  function clearCookies() {
    document.cookie.split(';').forEach(function (cookie) {
      var name = cookie.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      ['', ';domain=edificeapp.org', ';domain=.edificeapp.org', ';domain='+location.hostname].forEach(function (domain) {
        document.cookie = name+'=;max-age=0;path=/'+domain+';SameSite=Lax';
      });
    });
  }
  var banner = document.createElement('section');
  banner.className='analytics-choice';
  banner.setAttribute('aria-label','Website analytics preference');
  banner.innerHTML='<div><strong>Your cookie preferences</strong><p>We use optional analytics cookies to understand how our website is used and improve your experience. You can accept or reject them, and change your choice anytime. <a href="/privacy/#website-analytics">Learn more</a></p></div><div class="analytics-actions"><button type="button" data-choice="denied">Reject optional</button><button type="button" data-choice="granted">Accept cookies</button></div>';
  banner.hidden = saved === 'granted' || saved === 'denied';
  document.body.appendChild(banner);
  var settings = document.createElement('button');
  settings.type='button'; settings.className='analytics-settings'; settings.textContent='Cookie preferences';
  (document.querySelector('footer') || document.body).appendChild(settings);
  settings.addEventListener('click',function(){banner.hidden=false;banner.querySelector('button').focus();});
  banner.addEventListener('click',function(event){
    var button=event.target.closest('[data-choice]'); if(!button) return;
    var choice=button.getAttribute('data-choice');
    try {localStorage.setItem(KEY,choice);} catch (_) {}
    banner.hidden=true;
    if(choice==='granted') start();
    else {
      window['ga-disable-'+ID]=true;
      clearCookies();
      // Stop all loaded Google code after withdrawal, not just subsequent custom events.
      if(active) location.reload();
    }
    settings.focus();
  });
  document.addEventListener('click',function(event){
    if(!active || window['ga-disable-'+ID]) return;
    var link=event.target.closest('a[href]'); if(!link) return;
    var url; try {url=new URL(link.href);} catch(_){return;}
    if(url.hostname==='play.google.com' && url.pathname==='/store/apps/details' && url.searchParams.get('id')==='com.edifice.app') {
      window.gtag('event','app_download_click',{platform:'android',page_group:group,transport_type:'beacon'});
    }
  });
  if(saved==='granted') start();
})();
