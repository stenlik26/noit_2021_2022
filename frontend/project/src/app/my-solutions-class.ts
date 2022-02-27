export class MySolution{
    language: string = '';
    problem_public: boolean = false;
    code_id: string = '';
    problem_title: string = '';
    problem_id: string = '';
    solution_id: string = '';
    tests_passed: string = '';
    tests_total: string = '';
    timestamp: string = '';
    score: string = '';

    constructor(data: any){
        this.language = data.language;
        this.code_id = data._id.$oid;
        this.problem_public = data.problem.public;
        this.problem_title = data.problem.title;
        this.problem_id = data.problem._id.$oid;
        this.solution_id = data.solution_id.$oid;
        this.tests_passed = data.tests_passed;
        this.tests_total = data.tests_total;
        this.timestamp = data.timestamp;
        this.score = data.problem.score.toString();
    }

    get_test_score(): string{
        return this.tests_passed + " / " + this.tests_total;
    }

    get_score(): string{
        return this.score === "-1" ? "Няма поставена оценка": this.score
    }

    get_public(): string{
        return this.problem_public ? "Да" : "Не"
    }
}