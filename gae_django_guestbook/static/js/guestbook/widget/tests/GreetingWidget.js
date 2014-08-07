define([
    "doh/runner",
    "dojo/dom",
    'dojo/json',
    "/static/js/sinon/sinon.js",
    "/static/js/guestbook/widget/GreetingWidget.js",
    "/static/js/guestbook/widget/models/GreetingStore.js",
    "/static/js/guestbook/widget/GuestbookWidget.js"
], function(doh, dom, json, sinon, GreetingWidget, GreetingStore, GuestbookWidget){
    doh.register("TestGreetingWidget", [
        {
            name: "Test_Button_Delete_Called_Count",
            runTest: function(){
                var greetingWidget = new GreetingWidget();
                var mock = sinon.mock(greetingWidget);

                // expect: Called once
                mock.expects("_onclickDeleteBtn").once();
                // trigger
                greetingWidget.deleteButtonNode.onClick();
                mock.verify();
                mock.restore();
            }
        },
        {
            name: "Test_Button_Save_Called_Count",
            runTest: function(){
                var greetingWidget = new GreetingWidget();
                var mock = sinon.mock(greetingWidget);

                // expect: Called once
                mock.expects("_onclickSaveBtn").once();
                // trigger
                greetingWidget.contentNode.onChange();
                mock.verify();
                mock.restore();
            }
        }]);
});