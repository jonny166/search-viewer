(function(){
  'use strict';
  
  
  angular.module('searchapp-main',['ngRoute'])
    .config(function ($routeProvider) {
      $routeProvider
        .when('/', {
          templateUrl: 'main/main.html',
          controller: 'MainCtrl'
        });
    })
    .controller('MainCtrl', function ($scope) {
      $scope.articles = [
        {title: 'article 1', content: "some content here..."},
        {title: 'article 3', content: "some content here..."},
        {title: 'article 2', content: "some content here..."},
      ];
      
      $scope.tweets = [
        {author: 'tweet 1', date: "2014-01-01T23:28:56.782Z", 
         content: "someone said this..."},
        {author: 'tweet 3', date: "2014-04-01T23:28:56.782Z", 
         content: "someone said this..."},
        {author: 'tweet 2', date: "2014-02-01T23:28:56.782Z",
         content: "someone said this..."},
      ];
    })
  .controller('FormCtrl', function($scope, $window) {
    $scope.checkboxModel = {
      searchWikipedia : true,
      searchTwitter: false,
    };
    $scope.searchboxModel = {
      searchText: "test",
    };
    $scope.submit = function() {
      if($scope.searchboxModel.searchText) {
        $window.alert("You searched for " + $scope.searchboxModel.searchText);
        //TODO: Trigger search in appropriate APIs
      }
    };
  });
  
})();
