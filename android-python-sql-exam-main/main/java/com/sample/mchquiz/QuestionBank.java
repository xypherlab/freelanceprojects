package com.sample.mchquiz;

// This class contains a list of questions
import android.content.Context;
import android.os.AsyncTask;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class QuestionBank {

    ConnectionClass connectionClass;
    // declare list of Question objects
    List <Question> list = new ArrayList<>();
    MyDataBaseHelper myDataBaseHelper;
    public static String DATABASE_QUESTION = "questionBank.db";
    String question,c1,c2,c3,c4,answer;

    // method returns number of questions in list
    public int getLength(){
        return list.size();
    }

    // method returns question from list based on list index
    public String getQuestion(int a) {
       return list.get(a).getQuestion();
    }

    // method return a single multiple choice item for question based on list index,
    // based on number of multiple choice item in the list - 1, 2, 3 or 4
    // as an argument
    public String getChoice(int index, int num) {
        return list.get(index).getChoice(num-1);
    }

    //  method returns correct answer for the question based on list index
    public String getCorrectAnswer(int a) {
        return list.get(a).getAnswer();
    }


    public void initQuestions(Context context,String ipaddress,String subject,String quizsel) {
        myDataBaseHelper = new MyDataBaseHelper(context);
        connectionClass = new ConnectionClass();
        myDataBaseHelper.deleteInitialQuestion();

        try {


            Connection con = connectionClass.CONN(ipaddress,subject);
            String query=" select * from `"+quizsel+"`";
            Statement stmt = con.createStatement();
            ResultSet rs=stmt.executeQuery(query);
            while (rs.next())

            {
                question= rs.getString(3);
                c1=rs.getString(4);
                c2=rs.getString(5);
                c3=rs.getString(6);
                c4=rs.getString(7);
                answer=rs.getString(8);
                myDataBaseHelper.addInitialQuestion(new Question(question,
                        new String[]{c1, c2, c3, c4}, answer));
            }






        }
        catch (Exception ex)
        {

        }








        list = myDataBaseHelper.getAllQuestionsList();//get questions/choices/answers from database


    }

}