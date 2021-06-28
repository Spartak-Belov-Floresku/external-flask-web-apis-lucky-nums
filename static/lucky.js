/** processForm: get data from form and make AJAX call to our API. */
const processForm = async (form) => {

    // serializing data from form to the json obj
    const $json = $(form).serializeArray().reduce((obj, item) => { obj[item.name] = item.value; return obj; }, {})

    /// send data to the server
    return await axios.post(`/api/get-lucky-num`,{
        $json
    }).then( responce => {
        return responce
    }).catch(err => {
        console.log(err)
    });
}


/** handleResponse: deal with response from our lucky-num API. */

const handleResponse = resp => {

    const serverData = resp.data.resp
    
    ///checking status of responce from the server
    if(serverData[0].status){

        $lucky_results = $('#lucky-results');
        $lucky_results.empty();

            $lucky_results.append(`<p><b>Your birth year: ${JSON.parse(serverData[1]).number}</b><p>`);
                $lucky_results.append(`<p>${JSON.parse(serverData[1]).text}<p>`);
                    $lucky_results.append(`<p><b>Your lucky number: ${JSON.parse(serverData[2]).number}</b><p>`);
            $lucky_results.append(`<p>${JSON.parse(serverData[2]).text}<p>`);

    }else{
        /// if status false, notify user about issues

        serverData.map(elm => {
            if(elm['server']){
                $(`#server-err`).text(elm['server'])
            }else{
                Object.keys(elm).map(key => {
                    $(`#${key}-err`).text(elm[key])
                });
            }
        });
    }  
}



$("#lucky-form").submit(async (e) =>{
    e.preventDefault();
        const $form = e.target
            const $result = await processForm($form)
    handleResponse($result)
})
