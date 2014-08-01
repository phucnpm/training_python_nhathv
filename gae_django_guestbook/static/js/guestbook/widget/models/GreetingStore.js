/**
 * Created by NhatHV on 8/1/14.
 */
define([
    "dojo/_base/declare",
    "dojo/request",
    "dojo/cookie",
    "dojo/Deferred"
], function(declare, request, _cookie, Deferred){
    return declare("guestbook.GreetingStore", [Deferred], {
        // Create a new greeting
        createGreeting: function(guestbookName, greetingContent){
            var deferred = new Deferred();
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
                }).then(function(data){
                    console.log("The server returned: ", data);
                    deferred.resolve(data);
                }, function(error){
                    console.log("The server error: ", error.message);
                    deferred.reject(error);
                });
            } else {
                var error = {message: "This content is empty or length > 10 char"};
                deferred.reject(error);
            }
            return deferred.promise;
        },
        // Update a greeting
        updateGreeting: function(guestbookName, greetingId, greetingContent){
            var deferred = new Deferred();

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
                }).then(function(data){
                    console.log("The server returned: ", data);
                    deferred.resolve(data);
                }, function(error){
                    console.log("The server error: ", error.message);
                    deferred.reject(error);
                });
            } else {
                var error = {message: "This content is empty or length > 10 char"};
                deferred.reject(error);
            }
            return deferred.promise;
        },
        // Delete a greeting
        deleteGreeting: function(guestbookName, greetingId){
            var deferred = new Deferred();
            _url = "/api/guestbook/" + guestbookName + "/greeting/" + greetingId;
            request.del(_url, {
                headers: {
                    "X-CSRFToken": _cookie('csrftoken')
                }
            }).then(function(data){
                console.log("The server returned: ", data);
                deferred.resolve(data);
            }, function(error){
                console.log("The server error: ", error.message);
                deferred.reject(error);
            });
            return deferred.promise;
        },
        // get list greeting
        getListGreeting: function(guestbookName){
            var deferred = new Deferred();
            request.get("/api/guestbook/" + guestbookName + "/greeting/",
                {
                    handleAs: "json"
                }).then(function(data){
                    console.log("The server returned: ", data);
                    deferred.resolve(data);
                }, function(error){
                    console.log("The server error: ", error.message);
                    deferred.reject(error);
                });
            return deferred.promise;
        }
    })
});