const bcrypt = require('bcryptjs');
const axios = require('axios');

exports.handler = async (event, context) => {
    try {
        const data = event;
        const value = data.value;
        const saltRounds = 10;
        const hashedValue = await bcrypt.hash(value, saltRounds);
        console.log("Here is the output!!!")
        console.log(hashedValue);
        const response = {
            banner: "B00947866",
            result: hashedValue,
            arn: "arn:aws:lambda:us-east-1:982062056330:function:bcryptfunction",
            action: "bcrypt",
            value: value
        };
        await axios.post("https://v7qaxwoyrb.execute-api.us-east-1.amazonaws.com/default/end", response);

        return {
            statusCode: 200,
            body: response
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: 'Error: ' + error.message
        };
    }
};