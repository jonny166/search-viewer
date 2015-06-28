(function(){
  'use strict';
  
  
  angular.module('searchapp-main',['ngRoute', 'searchapp-main.services'])
    .config(function ($routeProvider) {
      $routeProvider
        .when('/search/:search_term/:search_wikipedia/:search_twitter', {
          templateUrl: 'main/main.html',
          controller: 'MainCtrl',
          reloadOnSearch: false,
        })
        .when('/search', {
          templateUrl: 'main/main.html',
          controller: 'MainCtrl',
          reloadOnSearch: false,
        });

    })
    .controller('MainCtrl', function ($scope, wikipediaService, twitterService) {
      $scope.articles = [];
      
      $scope.tweets = [];
    })
  .controller('FormCtrl', function($scope, $http, $window, wikipediaService,
                                   twitterService, $location, $routeParams) {

    $scope.submit = function() {
      //Clear the old results
      $scope.articles.length = 0;
      $scope.tweets.length = 0;

      // Store the form settings as url params
      $location.path('/search').search(
        {search_term: $scope.searchboxModel.searchText,
         search_wikipedia: $scope.checkboxModel.searchWikipedia,
         search_twitter: $scope.checkboxModel.searchTwitter,
        });


      if($scope.checkboxModel.searchWikipedia === true && 
         $scope.searchboxModel.searchText) {

        wikipediaService.search($scope.searchboxModel.searchText)
          .then(
            function(articles){
              console.log("GOT ARTICLES");
              console.log(articles);

              for (var articleIndex in articles){
                if (typeof articles[articleIndex].missing != 'undefined'){
                  $scope.articles.push({
                    title: articles[articleIndex].title,
                    content: "No matching article found",
                  });
                }
                else{
                  $scope.articles.push({
                    title: articles[articleIndex].title,
                    content: articles[articleIndex].extract
                  });
                  }
              }
            }
          )
        .catch(function(fallback) {
          //Wikipedia API failed
          console.log("Wikipedia Error");
          $scope.articles.length = 0;
          $scope.articles.push({
            title: "",
            content: fallback,
          });
        });
      }


      if($scope.checkboxModel.searchTwitter ===true && 
         $scope.searchboxModel.searchText) {
        twitterService.search($scope.searchboxModel.searchText)
          .then(
            function(tweets){
              console.log("GOT TWEETS");
              console.log(tweets);

              for (var tweetIndex in tweets.data){
                $scope.tweets.push({
                    author: tweets.data[tweetIndex].author,
                    content: tweets.data[tweetIndex].content
                });
              }
              
              if (tweets.data.length === 0){
                $scope.tweets.push({
                  author: "",
                  content: tweets.message,
                });
              }
            }
          )
        .catch(function(fallback) {
          //Twitter API failed
          console.log("Twitter Error");
          $scope.tweets.length = 0;
          $scope.tweets.push({
            author: "",
            content: fallback,
          });
        });
      }
    };

    //Inject the route params,
    $scope.checkboxModel = {
      searchWikipedia : $routeParams.search_wikipedia, 
      searchTwitter: $routeParams.search_twitter,
    };

    $scope.searchboxModel = {
      searchText: $routeParams.search_term,
    };

    if (typeof($scope.checkboxModel.searchWikipedia) ===  'undefined'){
      $scope.checkboxModel.searchWikipedia = true; //default
    }
    if (typeof($scope.checkboxModel.searchTwitter) ===  'undefined'){
      $scope.checkboxModel.searchTwitter = true; //default
    }

    if (typeof($scope.searchboxModel.searchText) ===  'undefined'){
      $scope.searchboxModel.searchText = "Cabbage"; //default
    }
    else{
      // Since a search term was specified, go ahead and submit it
      $scope.submit();
    }

  });
  
})();
