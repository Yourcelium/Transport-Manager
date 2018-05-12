new Vue({
    el: '#ride-form',
    delimiters: ["[[", "]]"],
    data: {
        first_name: "First",
        last_name: "Last",
        DOB_year: "Year",
        DOB_month: "Month",
        DOB_day: "Day",
        DOB: null,
        resident_found: false,
        resident: null,
        procedure: "procedure",
        destination: "destination",
        appointment_datetime: null,
        strecher: false,
        oxygen: false,
        oxygen_liters: 0,
        arranged_by: null,
    },
    methods: {
        searchResidents: function(){
            var self = this
            self.DOB = self.DOB_year + "-" + self.DOB_month + "-" + self.DOB_day
            $.get("/schedule/resident/search/" + "?full_name=" + self.first_name + "+" + self.last_name + "&DOB=" + self.DOB)
            .done(function(resident){
                self.resident = resident 
                self.resident = true
                 
            })
        },
        checkSubmit: function(){
            console.log("Im here")
            this.searchResidents()        
        } 
    }
    
})

