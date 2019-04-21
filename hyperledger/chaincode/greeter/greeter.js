'use strict';

const { Contract } = require('fabric-contract-api');

class Greeter extends Contract {
    async initLedger(ctx) {
        console.info('============= START : Initialize Ledger ===========');
        const greeting = { greet: false }

        await ctx.stub.putState("greeting", Buffer.from(JSON.stringify(greeting)));
        console.info('============= END : Initialize Ledger ===========');
    }

    async queryGreet(ctx) {
        const greetingBytes = await ctx.stub.getState("greeting");
        console.log(greetingBytes.toString());
        return greetingBytes.toString();
    }

    async toggleGreet(ctx){
        const greetingBytes = await ctx.stub.getState("greeting");
        var greeting = JSON.parse(greetingBytes.toString());
        greeting.greet = !greeting.greet;
        await ctx.stub.putState("greeting", Buffer.from(JSON.stringify(greeting)));
        console.log("State Changed to: " + greetingBytes.toString());

        await ctx.stub.setEvent('greetingEvent', Buffer.from(JSON.stringify(greeting)));
        console.info('============= END : changeGreet ===========');
    }
}
module.exports = Greeter;