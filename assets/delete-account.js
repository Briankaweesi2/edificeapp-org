/*
 * The web deletion route, which Google Play requires for any app with accounts — someone who
 * cannot sign in must still be able to ask.
 *
 * ## Why this only opens an email
 *
 * There is no endpoint behind this page. It is a static site; nothing here can record a request,
 * authenticate the person making it, or act on it. So the form composes the request and hands it
 * to the member's own mail client, which is a thing that genuinely happens rather than a thing we
 * claim happens.
 *
 * The page previously carried `onsubmit="handleDeletionSubmit(event)"` with no script defining it
 * anywhere. Submitting threw a ReferenceError, `preventDefault` never ran, and the form did a
 * native GET that put the member's email address in the URL — a deletion request that deleted
 * nothing and leaked the one field it collected. The panel it was supposed to reveal read "We have
 * recorded your account deletion request" and "A confirmation notice has been dispatched", neither
 * of which anything could have made true.
 *
 * Progressive enhancement: with no JavaScript the form is inert and the "Email us instead" link
 * beside it is the route. Nothing here is load-bearing for the requirement being met.
 */
(function () {
  var form = document.getElementById("deletionForm");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var email = (document.getElementById("userEmail") || {}).value || "";
    var reason = (document.getElementById("deletionReason") || {}).value || "";

    var body =
      "I am requesting deletion of my Edifice account.\n\n" +
      "Account email: " + email + "\n\n" +
      "Reason (optional): " + (reason || "—") + "\n\n" +
      "I understand this permanently deletes my account, journal entries, streaks and saved data " +
      "after the 7-day safety period.";

    var href =
      "mailto:supernaturalbrian@gmail.com" +
      "?subject=" + encodeURIComponent("Account Deletion Request - Edifice") +
      "&body=" + encodeURIComponent(body);

    var notice = document.getElementById("successMsg");
    if (notice) {
      notice.hidden = false;
      notice.style.display = "block";
    }
    window.location.href = href;
  });
})();
