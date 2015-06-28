(function(){
  'use strict';
  
  
  angular.module('searchapp-main.services',[])
    .service('wikipediaService', function($http, $q){
      return({
        search: search,
      });
      
      function search(searchTerm) {
        var request = $http({
          method: "jsonp",
          url: "http://en.wikipedia.org/w/api.php",
          params: {"action": "query",
                   callback: 'JSON_CALLBACK',
                   "prop": "extracts",
                   "exintro": "",
                   "explaintext": "",
                   "format": "json",
                   "titles": searchTerm,
                  }
        });
        
        return(request.then(handleSuccess, handleError));
      }
      
      function handleError(response){
        if(!angular.isObject(response.data) ||
           !response.data.message){
          return($q.reject("An error occurred searching wikipedia"));
        }
        
        return($q.reject(response.data.message));
      }
      
      function handleSuccess(response){
        return(response.data.query.pages);
      }
    })

    .service('twitterService', function($http, $q){
      return({
        search: search,
      });
      
      function search(searchTerm) {
        var request = $http({
          method: "get",
          url: "//localhost:5000/search_viewer/api/v1.0/search",
          params: {search_term: searchTerm,
                  }
        });
        
        return(request.then(handleSuccess, handleError));
      }
      
      function handleError(response){
        if(!angular.isObject(response.data) ||
           !response.data.message){
          return($q.reject("An error occurred searching twitter"));
        }
        
        return($q.reject(response.data.message));
      }
      
      function handleSuccess(response){
        console.log("GOT TWITTER DATA");
        console.log(response.data);
        return(response.data);
      }
    });


})();
                         
