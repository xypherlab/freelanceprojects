private static async Task ScrapeOffFormSkeletonFromGoogleFormsAsync(string yourGoogleFormsUrl)
{
	HtmlWeb web = new HtmlWeb();
	var htmlDoc = await web.LoadFromWebAsync(yourGoogleFormsUrl);

	var htmlNodes = htmlDoc.DocumentNode.SelectNodes("//script").Where(
		x => x.GetAttributeValue("type", "").Equals("text/javascript") &&
			 x.InnerHtml.Contains("FB_PUBLIC_LOAD_DATA_"));

	var fbPublicLoadDataJsScriptContent = htmlNodes.First().InnerHtml;

	// cleaning up "var FB_PUBLIC_LOAD_DATA_ = " at the beginning and 
	// and ";" at the end of the script text  
	var beginIndex = fbPublicLoadDataJsScriptContent.IndexOf("[", StringComparison.Ordinal);
	var lastIndex = fbPublicLoadDataJsScriptContent.LastIndexOf(";", StringComparison.Ordinal);
	var fbPublicJsScriptContentCleanedUp = fbPublicLoadDataJsScriptContent
						.Substring(beginIndex, lastIndex - beginIndex).Trim();

	var jArray = JArray.Parse(fbPublicJsScriptContentCleanedUp);

	var description = jArray[1][0].ToObject<string>();
	var title = jArray[1][8].ToObject<string>();
	var formId = jArray[14].ToObject<string>();

	Console.WriteLine("\n");
	Console.WriteLine("TITLE: " + title);
	Console.WriteLine("DESCRIPTION: " + description);
	Console.WriteLine("FORM ID: " + formId);
	Console.WriteLine("\n");

	var arrayOfFields = jArray[1][1];

	foreach (var field in arrayOfFields)
	{
		// Check if this Field is submittable or not
		// index [4] contains the Field Answer 
		// Submit Id of a Field Object 
		// ex: ignore Fields used as Description panels
		// ex: ignore Image banner fields
		if (field.Count() < 4 && !field[4].HasValues)
			continue;

		// Load the Question Field data
		var questionTextValue = field[1]; // Get Question Text
		var questionText = questionTextValue.ToObject<string>();

		var questionTypeCodeValue = field[3].ToObject<int>(); // Get Question Type Code   
		var isRecognizedFieldType = Enum.TryParse(questionTypeCodeValue.ToString(), 
						out GoogleFormsFieldTypeEnum questionTypeEnum);
		var questionType = questionTypeEnum.GetDescription();

		var answerOptionsList = new List<string>();
		var answerOptionsListValue = field[4][0][1].ToList(); // Get Answers List
		// List of Answers Available
		if (answerOptionsListValue.Count > 0)
		{
			foreach (var answerOption in answerOptionsListValue)
			{
				answerOptionsList.Add(answerOption[0].ToString());
			}
		}

		var answerSubmitIdValue = field[4][0][0]; // Get Answer Submit Id
		var isAnswerRequiredValue = field[4][0][2]; // Get if Answer is Required to be Submitted
		var answerSubmissionId = answerSubmitIdValue.ToObject<string>();
		var isAnswerRequired = isAnswerRequiredValue.ToObject<int>() == 1 ? true : false; // 1 or 0

		// Printing Field Data
		Console.WriteLine("QUESTION: " + questionText);
		Console.WriteLine("TYPE: " + questionType);
		Console.WriteLine("IS REQUIRED: " + (isAnswerRequired ? "YES" : "NO"));
		if (answerOptionsList.Count > 0)
		{
			Console.WriteLine("ANSWER LIST: ");
			foreach (var answerOption in answerOptionsList)
			{
				Console.WriteLine($"-{answerOption.ToString()}");
			}
		}
		Console.WriteLine("SUBMITID: " + answerSubmissionId + "\n");

		Console.WriteLine("----------------------------------------\n");
	}
}