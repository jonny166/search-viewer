(function(){
	'use strict';

	angular.module('searchapp', [ 'ngRoute','searchapp-main',
				      'searchapp-main.services','templates' ])
	  .config(function ($routeProvider) {
	    $routeProvider
	      .otherwise({
	        redirectTo: '/search'
	      });
	  });
	  
})();
