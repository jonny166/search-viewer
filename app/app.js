(function(){
	'use strict';

	angular.module('searchapp', [ 'ngRoute','searchapp-main','templates' ])
	  .config(function ($routeProvider) {
	    $routeProvider
	      .otherwise({
	        redirectTo: '/'
	      });
	  });
	  
})();