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
    "dijit/form/ValidationTextBox",
    "dijit/form/Button",
    "dojo/text!./templates/SignFormWidget.html"
], function(declare, baseFx, lang, domStyle, on, _request, _cookie, _WidgetBase,
            _TemplatedMixin, _WidgetsInTemplateMixin, ValidationTextBox, Button, template){
    return declare("guestbook.SignFormWidget", [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin ], {
        // Our template - important!
        templateString: template,
        widgetsInTemplate: true,

        // default value
        guestbookName: "default_guestbook",

        postCreate: function(){
            this.inherited(arguments);
            this.own(
                on(this.signButtonNode, "click", lang.hitch(this, "_onclickSignBtn"))
            );
        },

        _onclickSignBtn : function(){
            this.signNewGreeting(this.GuestbookWidgetParent,
                this.guestbookNameNode.value,
                this.contentNode.value);
        },

        signNewGreeting: function(guestbookWidget, guestbookName, greetingContent){
            var _contentLength = greetingContent.length;
            if (_contentLength > 0 && _contentLength <= 10){
                _request.post("/api/guestbook/" + guestbookName + "/greeting/", {
                    data: {
                        guestbook_name: guestbookName,
                        content: greetingContent
                    },
                    headers: {
                        "X-CSRFToken": _cookie('csrftoken')
                    }
                }).then(function(text){
                    console.log("The server returned: ", text);
                    guestbookWidget.reloadListGreeting(guestbookName);
                });
            } else {
                alert("Error = This content is empty or length > 10");
            }
        },

        _setGuestbookNameAttr: function(guestbookName){
            this.guestbookNameNode.value = guestbookName;
        }
    });
});