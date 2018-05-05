new Vue({
    el: '#trips-future',
    delimiters: ["[[", "]]"],
    data: {
        trips : [],
        loading: false,
    },
    methods: {
        getTodayTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/api_triplist_unscheduled')
            .done(function(trips){
                self.trips = trips
                self.loading = false;
            })    
        }
    },
    created: function(){
        this.getTodayTrips()
    }
})