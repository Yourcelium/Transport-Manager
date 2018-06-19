new Vue({
    el: '#trips-future',
    delimiters: ["[[", "]]"],
    data: {
        all_trips : null,
        today_trips : null,
        tomorrow_trips : null,
        week_trips: null,
        week_plus_trips: null,
        display_trips: null,
        loading: false,
        resident: null,
        floor : 0,
    },
    methods: {
        getTodayTrips: function(){
            var self = this
            $.get('/schedule/trip/api_trip_list?floor=' + '2&timerange=' + 'today')
            .done(function(trips){
                console.log(trips)
                self.today_trips = trips
            })    
        },
        getTomorrowTrips: function(){
            var self = this
            $.get('/schedule/trip/api_trip_list?floor=' + '2&timerange=' + 'tomorrow')
            .done(function(trips){
                console.log(trips)
                self.tomorrow_trips = trips
            })    
        },
        getWeekTrips: function(){
            var self = this
            $.get('/schedule/trip/api_trip_list?floor=' + '2&timerange=' + 'week')
            .done(function(trips){
                console.log(trips)
                self.week_trips = trips
            })    
        },
        getWeekPlusTrips: function(){
            var self = this
            $.get('/schedule/trip/api_trip_list?floor=' + '2&timerange=' + 'week_plus')
            .done(function(trips){
                console.log(trips)
                self.week_plus_trips = trips
            })    
        },
        selectTrip: function(event) {
            var self = this
            var trip_id = event.target.attributes["data-id"]["value"]
            window.location.url = 'trip/api/detail&tripID=' + trip_id
        }
    },
    created: function(){
        this.getTodayTrips()
        this.getTomorrowTrips()
        this.getWeekTrips()
        this.getWeekPlusTrips()
    }
})