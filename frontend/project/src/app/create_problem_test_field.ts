export class TestField{
    test_num = '';
    input = '';
    output = '';
    is_hidden: boolean = false;
    time_limit = '';
    
    constructor(test_num: string, input: string, output: string, is_hidden: boolean, time_limit: string)
    {
        this.test_num = test_num;
        this.input = input;
        this.output = output;
        this.is_hidden = is_hidden;
        this.time_limit = time_limit;
    }

    setTest(input: string, output: string, is_hidden: boolean, time_limit: string): void{
        this.input = input;
        this.output = output;
        this.is_hidden = is_hidden;
        this.time_limit = time_limit;
    }

    get_test_num(): string{
        return this.test_num;
    }

    get_input(): string{
        return this.input;
    }

    get_output(): string{
        return this.output;
    }

    get_is_hidden(): boolean{
        return this.is_hidden;
    }

    get_time_limit(): string{
        return this.time_limit;
    }

}