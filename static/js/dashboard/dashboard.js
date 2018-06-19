new Vue({
    el: '#dashboard',
    delimiters: ["[[", "]]"],
    data: {
        todayTrips : [],
        futureTrips : [],
        days: 7,
        floor: 0,
        loading: false,
        resident: 'all',
    },
    methods: {
        getTodayTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/today' + '?floor=' + self.floor)
            .done(function(todayTrips){
                self.todayTrips = todayTrips
                console.log(self.todayTrips)         
                self.loading = false;
            })    
        },
        getFutureTrips: function(){
            this.loading=true;
            var self = this
            $.get('/schedule/trip/future' + '?days=' + self.days + '&floor=' + self.floor)
            .done(function(futureTrips){
                self.futureTrips = futureTrips
                console.log(self.futureTrips)
                self.loading = false;
            })    
        },

        checkSubmitDays: function(event){
            if (event.code === 'Enter'){
                this.getFutureTrips()
            }
        },

        checkSubmitFloor: function(event){
            if (event){
                this.getTodayTrips()
                this.getFutureTrips()
            }
        }
    },
    created: function(){
        this.getTodayTrips()
        this.getFutureTrips()
    }
})
