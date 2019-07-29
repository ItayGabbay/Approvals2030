'use strict';

var app = angular.module('approvals', ['ngRoute']);


app.config(function ($routeProvider, $locationProvider, $httpProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/views/index.html',
        controller: 'contr'
    })
     .otherwise({
        redirectTo: '/'
     });

     $locationProvider.hashPrefix('');
});

app.controller('contr',  ['$scope', '$http', function($scope, $http) {
    $scope.apprs = [{'id':1}];
    $http.get('api/getAllPersons').then(function(res) {
        $scope.approvals = res.data;
    }, function (err) {
        console.log(err);
    });     
}]);
