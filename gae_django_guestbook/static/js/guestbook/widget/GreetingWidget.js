/**
 * Created by NhatHV on 7/28/14.
 */
define([
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/dom",
    "dojo/dom-style",
    "dojo/mouse",
    "dojo/on",
    "dojo/request",
    "dojo/cookie",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/InlineEditBox",
    "dojo/text!./templates/GreetingWidget.html"
], function(declare, baseFx, lang, dom, domStyle, mouse, on, _request, _cookie,
            _WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin, InlineEditBox, template){
    return declare("guestbook.Greeting", [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        author: "No Name",
        content: "No content",
        updatedBy: "No updated by",
        updatedDate: "No update date",

        guestbookName: "default_guestbook",

        // Our template - important!
        templateString: template,

        // A class to be applied to the root node in our template
        baseClass: "guestbookWidget",

        // A reference to our background animation
        mouseAnim: null,

        // Colors for our background animation
        baseBackgroundColor: "#fff",
        mouseBackgroundColor: "#def",
        editBackgroundColor: "#000",

        postCreate: function(){
            // Get a DOM node reference for the root of our widget
            var domNode = this.domNode;
            // Run any parent postCreate processes - can be done at any point
            this.inherited(arguments);

            // Set our DOM node's background color to white -
            // smoothes out the mouseenter/leave event animations
            domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
            // Set up our mouseenter/leave events
            // Using dijit/Destroyable's "own" method ensures that event handlers are unregistered when the widget is destroyed
            // Using dojo/mouse normalizes the non-standard mouseenter/leave events across browsers
            // Passing a third parameter to lang.hitch allows us to specify not only the context,
            // but also the first parameter passed to _changeBackground
            this.own(
                // change background
                on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor, domNode)),
                on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor, domNode)),

                // handle button Delete
                on(this.deleteButtonNode, "click", lang.hitch(this, "_onclickDeleteBtn"))
                // button save in InLineEditText
                ,on(this.contentNode, "change", lang.hitch(this, "_onclickSaveBtn"))
            );
        },

        _changeBackground: function(newColor, node) {
            // If we have an animation, stop it
            if (this.mouseAnim) {
                this.mouseAnim.stop();
            }

            // Set up the new animation
            this.mouseAnim = baseFx.animateProperty({
                node: node,
                properties: {
                    backgroundColor: newColor
                },
                onEnd: lang.hitch(this, function() {
                    // Clean up our mouseAnim property
                    this.mouseAnim = null;
                })
            }).play();
        },

        _onclickDeleteBtn: function(){
            var _guestbookParent = this.GuestbookWidgetParent;
            var _guestbookName = this.guestbookName;
            _url = "/api/guestbook/" + _guestbookName + "/greeting/"
                    + this.greetingIdNode.value;
            _request.del(_url, {
                headers: {
                    "X-CSRFToken": _cookie('csrftoken')
                }
            }).then(function(text){
                console.log("The server returned: ", text);
                _guestbookParent.reloadListGreeting(_guestbookName);
            });
        },

        _onclickSaveBtn: function(){
            content = this.contentNode.value;
            if (content.length > 0 && content.length <= 10){
                var _guestbookParent = this.GuestbookWidgetParent;
                var _guestbookName = this.guestbookName;
                _url = "/api/guestbook/" + _guestbookName + "/greeting/"
                    + this.greetingIdNode.value;
                _request.put(_url, {
                    data: {
                        greeting_author: "None",
                        greeting_content: this.contentNode.value
                    },
                    headers: {
                        "X-CSRFToken": _cookie('csrftoken')
                    }
                }).then(function(text){
                    console.log("The server returned: ", text);
                    _guestbookParent.reloadListGreeting(_guestbookName);
                });
            } else {
                alert("Error = This content is empty or length > 10")
            }
        }
        , setHiddenDeleteNode:function(hidden){
            if (hidden){
                domStyle.set(this.deleteButtonNode.domNode, 'visibility', 'hidden');
            } else {
                domStyle.set(this.deleteButtonNode.domNode, 'visibility', 'visible');
            }
        }
        , setDisabledEditor: function(disabled){
            this.contentNode._setDisabledAttr(disabled);
        }
        , setGuestbookName: function(guestbookName){
            this.guestbookName = guestbookName;
        }
        , setGuestbookParent:function(guestbookParent){
            this.GuestbookWidgetParent = guestbookParent;
        }
    });
});