/**
 * Created by NhatHV on 8/1/14.
 */
define([
    "dojo/_base/declare",
    "dojo/request",
    "dojo/cookie"
], function(declare, request, _cookie){
    return declare("guestbook.GreetingStore", [], {
        // Create a new greeting
        createGreeting: function(guestbookWidget, guestbookName, greetingContent){
            var _contentLength = greetingContent.length;
            if (_contentLength > 0 && _contentLength <= 10){
                _url = "/api/guestbook/" + guestbookName + "/greeting/";
                request.post(_url, {
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
                }, function(error){
                    console.log("The server error: ", error.message);
                });
            } else {
                alert("Error = This content is empty or length > 10 chars");
            }
        },
        // Update a greeting
        updateGreeting: function(guestbookWidget, guestbookName, greetingId, greetingContent){
            var _contentLength = greetingContent.length;
            if (_contentLength > 0 && _contentLength <= 10){
                _url = "/api/guestbook/" + guestbookName + "/greeting/" + greetingId;
                request.put(_url, {
                    data: {
                        greeting_author: "None",
                        greeting_content: greetingContent
                    },
                    headers: {
                        "X-CSRFToken": _cookie('csrftoken')
                    }
                }).then(function(text){
                    console.log("The server returned: ", text);
                    guestbookWidget.reloadListGreeting(guestbookName);
                }, function(error){
                    console.log("The server error: ", error.message);
                });
            } else {
                alert("Error = This content is empty or length > 10 chars")
            }
        },
        // Delete a greeting
        deleteGreeting: function(guestbookWidget, guestbookName, greetingId){
            _url = "/api/guestbook/" + guestbookName + "/greeting/" + greetingId;
            request.del(_url, {
                headers: {
                    "X-CSRFToken": _cookie('csrftoken')
                }
            }).then(function(text){
                console.log("The server returned: ", text);
                guestbookWidget.reloadListGreeting(guestbookName);
            }, function(error){
                console.log("The server error: ", error.message);
            });
        }
    })
});