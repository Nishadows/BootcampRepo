// @TODO: YOUR CODE HERE!
d3.csv("/assets/data/data.csv", function(error, povertydata){
    if (error) throw error;

    povertydata.forEach(function (pdata) {
       
    console.log(pdata);

    });
});


