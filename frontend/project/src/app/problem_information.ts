import { TestField } from "./create_problem_test_field";

export class ProblemInformation{
    start_date = '';
    end_date = '';
    test_fields: Array<TestField> = new Array<TestField>();
    problem_text = '';
    time_limit = '';
    title ='';

    constructor(start_date: string, end_date: string, problem_text: string, time_limit: string, title: string)
    {
        this.start_date = start_date;
        this.end_date = end_date;
        this.problem_text = problem_text;
        this.time_limit = time_limit;
        this.title = title;
    }

    get_problem_text(): string{
        return this.problem_text;
    }

    get_problem_title(): string{
        return this.title;
    }

}