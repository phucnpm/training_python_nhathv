/**
 * Created by NhatHV on 8/5/14.
 */
define([
    "doh/runner",
    "dojo/dom",
    "/static/js/sinon/sinon.js",
    "/static/js/guestbook/widget/SignFormWidget.js"
], function(doh, dom, sinon, SignFormWidget){
    doh.register("TestSignFormWidget", [
        {
            name: "Button_Sign_onclick_count",
            setUp: function(){
            },
            runTest: function(){
                signFormWidget = new SignFormWidget();
                onclickSignBtnSpy = sinon.spy(signFormWidget, "_onclickSignBtn");
                signFormWidget.signButtonNode.onClick();
                doh.t(onclickSignBtnSpy.calledOnce);
            }
        }]);
});