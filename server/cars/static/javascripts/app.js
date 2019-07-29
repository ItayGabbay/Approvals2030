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
    $scope.apprs = [];
    
    $http.get('api/getAllPersons').then(function(res) {
        $scope.approvals = res.data;
    }, function (err) {
        console.log(err);
    });

    $scope.update_approval = function(approval_id, is_authorized) {
        $http.get('api/updateApproval?id=' + approval_id + "&is_authorized=" + (is_authorized=='True')).then(function(res) {
            $scope.approvals = res.data;
        }, function (err) {
            console.log(err);
        });
    }
}]);
