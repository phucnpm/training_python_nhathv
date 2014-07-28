/**
 * Created by NhatHV on 7/28/14.
 */
define([
    "dojo/_base/declare",
    "dojo/_base/fx",
    "dojo/_base/lang",
    "dojo/dom-style",
    "dojo/on",
    "dijit/_WidgetBase",
    "dijit/_OnDijitClickMixin",
    "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/text!./templates/SignFormWidget.html"
], function(declare, baseFx, lang, domStyle, on, _WidgetBase, _OnDijitClickMixin,
            _TemplatedMixin, _WidgetsInTemplateMixin, template){
    return declare([_WidgetBase, _OnDijitClickMixin,
        _TemplatedMixin, _WidgetsInTemplateMixin ], {
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
            alert(this.contentNode.value);
        }

    });
});