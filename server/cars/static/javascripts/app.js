'use strict';

var app = angular.module('approvals', ['ngRoute']);


app.controller('myCtrl', function($scope, $http) {
    $http.get('api/getAllPerssons').then(function(res) {
        $scope.approvals = res.data;
    }, function (err) {
        console.log(err);
    });     
});


app.config(function ($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/', {
        controller: 'myCtrl'
    })
     .otherwise({
        redirectTo: '/'
     });

     $locationProvider.hashPrefix('');
});
