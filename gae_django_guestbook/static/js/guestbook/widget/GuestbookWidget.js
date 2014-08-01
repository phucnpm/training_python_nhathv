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

        postCreate: function () {
            // handle event
            this.own(
                on(this.switchButtonNode, "click", lang.hitch(this, "_onclickSwitchBtn"))
            );
            // load data
            this._showListGreeting(this.guestbookName);
            this._showSignGreetingForm();
        },

        _showSignGreetingForm: function(){
            this.signFormWidget = new SignFormWidget({GuestbookWidgetParent:this});
            this.signFormWidget.placeAt(this.signFormContainerNode);
            this.signFormWidget.startup();
        },

        _showListGreeting: function(guestbookName){
            var _isAdmin = dom.byId("is_user_admin").value;
            var _userLogin = dom.byId("user_login").value;
            var _guestbookWidgetParent = this;
            request.get("/api/guestbook/" + guestbookName + "/greeting/",
                {
                    handleAs: "json"
                }).then(function(data){
                    var _newDocFrag = document.createDocumentFragment();
                    arrayUtil.forEach(data.greetings, function(greeting){
                        var greetingWidget = new GreetingWidget(greeting);
                        // show button delete for admin
                        if (_isAdmin.toLowerCase() == "true"){
                            greetingWidget.setHiddenDeleteNode(false);
                            greetingWidget.setDisabledEditor(false);
                        }
                        // show button edit if author written
                        if (_userLogin == greeting.author){
                            greetingWidget.setDisabledEditor(false);
                        }
                        // set guestbook name
                        greetingWidget.setGuestbookName(guestbookName);
                        greetingWidget.setGuestbookParent(_guestbookWidgetParent);

                        greetingWidget.placeAt(_newDocFrag);
                    });
                    domConstruct.place(_newDocFrag, "greetingsContainer");
                });
        },

        _onclickSwitchBtn: function(){
            var _guestbookNameLength = this.guestbookNameNode.value;
            if (_guestbookNameLength > 0 && _guestbookNameLength <= 20){
                this.reloadListGreeting(this.guestbookNameNode.value);
                // set guestbook name for Sign form
                this.signFormWidget._setGuestbookNameAttr(this.guestbookNameNode.value);
            } else {
                alert("Error: Guestbook name is empty or length > 20 chars")
            }
        },

        _removeAllGreeting: function(){
            var greetingsContainer = dom.byId("greetingsContainer");
            greetingsContainer.innerHTML = "";
        },

        _setGuestbookNameAttr: function(guestbookName){
            this.guestbookNameNode.set("value", guestbookName);
        },

        reloadListGreeting:function(guestbookName){
            this._removeAllGreeting();
            this._showListGreeting(guestbookName);
        }
    });
});