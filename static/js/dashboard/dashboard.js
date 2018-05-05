new Vue({
    el: '#trips-today',
    delimiters: ["[[", "]]"],
    data: {
        trips : [],
        loading: false,
    },
    methods: {
        getTodayTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/today')
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
