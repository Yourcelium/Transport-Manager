new Vue({
    el: '#ride-form',
    delimiters: ["[[", "]]"],
    data: {
        first_name: "",
        last_name: "",
        DOB: "",
        resident_found: false,
        resident: null,
        procedure: "",
        
        destination: "",
        destination_list: null,
        destination_selected:false,
        search: "",
        new_destination: false,
        
        appointment_datetime: null,
        strecher: false,
        wheelchair: false,
        oxygen: false,
        oxygen_liters: 0,
        arranged_by: null,
        error : false,
        error_message: "",
        
    },
    computed: {
        destinationFilter: function() {
            return this.findBy(this.destination_list, this.search, 'address')
        }
    },
    methods: {
        searchResidents: function(){
            var self = this
            self.DOB = self.DOB.replace(/\/|_/g,'-');
            $.get("/schedule/resident/search/" + "?first_name=" + self.first_name + "&lastname=" + self.last_name + "&DOB=" + self.DOB)
            .done(function(resident){
                self.error = false
                self.resident = resident 
                self.resident_found = true
                console.dir(resident)    
            })
            .fail(function(data, textStatus, xhr) {
                self.error = true
                self.error_message = "Resident Not Found"
            })
        },
        checkSubmit: function(){
            this.searchResidents()        
        },
        getDestinations: function(){
            var self = this
            $.get("/schedule/destination/list")
            .done(function(destinations){
                self.destination_list = destinations
                console.log(self.destination_list)
                console.log('I ran')
            })
        },
        findBy: function (list, value, column) {
            return list.filter(function (item) {
                return item[column].includes(value)
            })
        },
        newDestination: function(){
            this.new_destination = true
        } 
    },
    created: function(){
        this.getDestinations()
    },
    
    
})

