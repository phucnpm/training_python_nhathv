/**
 * Created by NhatHV on 7/30/14.
 */

define([
    "dojo/_base/declare",
    "dojo/_base/lang",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/request",
    "dojo/on",
    "dojo/dom",
    "dojo/dom-construct",
    "dojo/_base/array",
    "/static/js/guestbook/widget/GreetingWidget.js",
    "/static/js/guestbook/widget/SignFormWidget.js",
    "dojo/text!./templates/GuestbookWidget.html"
], function(declare, lang, _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
            request, on, dom, domConstruct,
            arrayUtil, GreetingWidget, SignFormWidget, template){
    return declare("guestbook.GuestbookWidget", [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin,
        GreetingWidget, SignFormWidget], {
        // Our template - important!
        templateString: template,
        widgetsInTemplate: true,

        // Defaut value
        guestbookName: "default_guestbook",

        constructor: function () {
        },

        postMixInProperties: function () {

        },

        postCreate: function () {
            // handle event
            this.own(
                on(this.switchButtonNode, "click", lang.hitch(this, "_onclickSwitchBtn"))
            );
            // load data
            this._showListGreeting("default_guestbook", this.greetingsContainerNode);
            this._showSignGreetingForm();
        },

        startup: function () {
        },

        _showSignGreetingForm: function(){
            this.signFormWidget = new SignFormWidget({GuestbookWidgetParent:this});
            this.signFormWidget.placeAt(this.signFormContainerNode);
            this.signFormWidget.startup();
        },

        _showListGreeting: function(guestbook_name, greetingsContainerNode){
            var is_admin = dom.byId("is_user_admin").value;
            var user_login = dom.byId("user_login").value;
            var guestbookWidgetParent = this;
            request.get("/api/guestbook/" + guestbook_name + "/greeting/",
                {
                    handleAs: "json"
                }).then(function(data){
                    arrayUtil.forEach(data.greetings, function(greeting){
                        var greetingWidget = new GreetingWidget(greeting);
                        // show button delete for admin
                        if (is_admin.toLowerCase() == "true"){
                            greetingWidget.setHiddenDeleteNode(false);
                            greetingWidget.setDisabledEditor(false);
                        }
                        // show button edit if author written
                        if (user_login == greeting.author){
                            greetingWidget.setDisabledEditor(false);
                        }
                        // set guestbook name
                        greetingWidget.setGuestbookName(guestbook_name);
                        greetingWidget.setGuestbookParent(guestbookWidgetParent);

                        greetingWidget.placeAt(greetingsContainerNode);
                        greetingWidget.startup();
                    });
                });
        },

        _onclickSwitchBtn: function(){
            this.reloadListGreeting(this.guestbookNameNode.value, this.greetingsContainerNode);
            // set guestbook name for Sign form
            this.signFormWidget._setGuestbookNameAttr(this.guestbookNameNode.value);
        },

        _removeAllGreeting: function(){
            while (this.greetingsContainerNode.hasChildNodes()) {
                this.greetingsContainerNode.removeChild(this.greetingsContainerNode.lastChild);
            }
        },

        _setGuestbookNameAttr: function(guestbook_name){
            this.guestbookNameNode.set("value", guestbook_name);
        },

        reloadListGreeting:function(guestbook_name, greetingsContainerNode){
            this._removeAllGreeting();
            this._showListGreeting(guestbook_name, greetingsContainerNode);
        }
    });
});