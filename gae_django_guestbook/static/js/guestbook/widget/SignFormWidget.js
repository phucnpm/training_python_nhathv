/**
 * Created by NhatHV on 7/28/14.
 */
define([
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/on",
    "dojo/request",
    "dojo/cookie",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/text!./templates/SignFormWidget.html"
], function(declare, baseFx, lang, domStyle, on, _request, _cookie, _WidgetBase,
            _TemplatedMixin, _WidgetsInTemplateMixin, template){
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin ], {
        // Our template - important!
        templateString: template,
        widgetsInTemplate: true,

        // A class to be applied to the root node in our template
        baseClass: "signGreetingWidget",
        postCreate: function(){
            this.own(
                on(this.signButtonNode, "click", lang.hitch(this, "_onclickSignBtn"))
            );
        },
        _onclickSignBtn : function(){
            _contentLength = this.contentNode.value.length;
            if (_contentLength > 0 && _contentLength <= 10){
                _request.post("/api/guestbook/default_guestbook/greeting/", {
                    data: {
                        guestbook_name: this.guestbookNameNode.value,
                        content: this.contentNode.value
                    },
                    headers: {
                        "X-CSRFToken": _cookie('csrftoken')
                    }
                }).then(function(text){
                    console.log("The server returned: ", text);
                });
            } else {
                alert("Error = This content is empty or length > 10");
            }
        }
    });
});