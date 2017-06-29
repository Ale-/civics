angular.module('civics.directives', [])

.directive('social', function(){
    return {
      restrict: 'A',
      templateUrl: 'static/civics/angular/views/social_widget.html'
    };
});
