
new Vue({
    el: '#trips-future',
    delimiters: ["[[", "]]"],
    data: {
        trips : [],
        days: 7,
        floor: 0,
        loading: false,
    },
    methods: {
        getFutureTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/future' + '?days=' + self.days + '?floor=' + self.floor)
            .done(function(trips){
                self.trips = trips
                self.loading = false;
            })    
        },
        
        checkSubmitDays: function(event){
            if (event.code === 'Enter'){
                this.getFutureTrips()
            }
        }
        
    },
    created: function(){
        this.getFutureTrips()
    }
})