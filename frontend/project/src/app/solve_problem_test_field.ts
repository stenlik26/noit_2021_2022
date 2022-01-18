export class TestField{
    test_num = '';
    input = '';
    output = '';
    expected_output = '';
    diff = '';
    time_limit = 0;
    
    constructor(
        test_num: string,
        input: string,
        output: string, 
        expected_output: string,
        diff: string, 
        time_limit: number)
    {
        this.test_num = test_num;
        this.input = input;
        this.output = output;
        this.time_limit = time_limit;
        this.expected_output = expected_output;
        this.diff = diff;
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

    get_time_limit(): number{
        return this.time_limit;
    }

    get_expected_output(): string{
        return this.expected_output;
    }

    get_diff(): string{
        return this.diff;
    }

}