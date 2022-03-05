import { TestField } from './solve_problem_test_field';

export class SubmissionInfo {
    submission_id: string = '';
    author_id: string = '';
    code: string = '';
    comments: Array<any> = new Array<any>();
    language: string = '';
    solution_id: string = '';
    tests_failed: Array<TestField> = new Array<TestField>();
    tests_passed: number = -1;
    tests_total: number = -1;
    timestamp: string = '';

    constructor(json_data: any) {

        if (json_data.name !== undefined) {
            this.submission_id = json_data._id;
            this.author_id = json_data.author_id;
            this.code = json_data.code;
            this.comments = json_data.comments;
            this.language = json_data.language;

            this.timestamp = json_data.timestamp;
        }
        else {


            this.submission_id = json_data._id;
            this.author_id = json_data.author_id;
            this.code = json_data.code;
            this.comments = json_data.comments;
            this.language = json_data.language;
            this.solution_id = json_data.solution_id;

            let num = 1;
            json_data.test_failed.forEach((element: any) => {
                this.tests_failed.push(new TestField(
                    num.toString(),
                    element.input,
                    element.test_output,
                    element.expected_stdout,
                    element.diff,
                    0));
                num++;
            });

            this.tests_passed = json_data.tests_passed;
            this.tests_total = json_data.tests_total;
            this.timestamp = json_data.timestamp;
        }
    }

    get_code(): string {
        return this.code;
    }

    get_language(): string {
        return this.language;
    }

    get_timestamp(): string {
        return this.timestamp;
    }

    get_tests_passed(): number {
        return this.tests_passed;
    }

}
