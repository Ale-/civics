angular.module('civics.xls_downloader', [])

.service('XlsDownloader', function(){

    /**
     *   Download XLS with filtered initiatives
     */
    this.get = function(section, selected_categories){

        // Check section and build base URL for the query
        var base_url = "/api/initiatives_xls?topics=";
        if(section == 'events')
            base_url = "/api/events_xls?topics=";

        // Build url
        for(var i in selected_categories.topics){
            var topic = selected_categories.topics[i]
            if(topic)
              base_url += topic.toUpperCase() + ",";
        }
        if(section == 'initiatives'){
            base_url += "&spaces=";
            for(var i in selected_categories.spaces){
              var space = selected_categories.spaces[i];
              if(space)
                base_url += space.toUpperCase() + ",";
            }
        } else {
            base_url += "&activities=";
            for(var i in selected_categories.activities){
                activity = selected_categories.activities[i];
                if(activity)
                  base_url += activity.toUpperCase() + ",";
            }
        }
        base_url += "&agents=";
        for(var i in selected_categories.agent){
            agent = selected_categories.agent[i];
            if(agent)
              base_url += agent.toUpperCase() + ",";
        }

        // Get items in new window
        window.open(base_url);
  };

  return this;
})
