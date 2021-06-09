import React, { useState, useEffect, useContext } from "react";
import { Formik, Form, Field, FieldArray } from "formik";
import Button from "../../components/Button";
import DashboardLayout from "../../components/DashboardLayout/DashboardLayout";
import * as yup from "yup";
import Checkbox from "./../../components/Checkbox";
import Grid from "@material-ui/core/Grid";
import DateFnsUtils from "@date-io/date-fns";
import { ImCross } from "react-icons/im";
import { formatISO } from "date-fns";
import { Tooltip } from "@material-ui/core";
import { BsCloudUpload } from "react-icons/bs";
import Image from "./../../components/Image";
import "./statics/css/quizCreator.css";
import colorscheme from "../../utils/colors";
import { UserContext } from "../../utils/Contexts/UserContext";
import callAPI from "../../utils/API";
import useAPI from "../../utils/useAPI";
import { AiOutlineFileImage } from "react-icons/ai";
import configs from "../../utils/configs";
import { fromUnixTime } from "date-fns/esm";
import { DatePicker, TimePicker } from "../../components/CustomDateTime";
import CustomTextField from "../../components/CustomTextField";

const validationSchema = yup.object({
  quiz_title: yup.string("Enter the title of the quiz"),
  quiz_description: yup.string("Enter description"),
  whoseQuizInfo: yup.object().required().typeError("Group required"),
});

let answerList = [];
const groupFormatter = (response) => {
  if (!response.data.length) {
    return [];
  }
  let responseData = [];
  responseData = response.data.map((data) => {
    let formattedData = {
      id: data.id,
      semester: data.sem,
      program_id: data.program.id,
      program_name: data.program.name,
      course_id: data.course[0].id,
      course_code: data.course[0].course_code,
      course_name: data.course[0].course_name,
    };

    return formattedData;
  });

  return responseData;
};

const QuizCreator = () => {
  const { user } = useContext(UserContext);
  const groupList = [];

  const [groups, groupsComplete] = useAPI(
    { endpoint: "/api/v1/group/" },
    groupFormatter
  );

  if (groups && groups.length && groupsComplete) {
    groups.map((group, index) => {
      groupList.push({
        name: `${group.program_name}, Sem ${group.semester} [Course ${group.course_code}]`,
        value: { group: group.id, course: group.course_id },
      });
    });
  }

  const questionInitialValue = {
    question_text: "",
    question_image: "",
    options: [],
  };
  const handleSubmit = (values) => {
    console.log(values);
  };
  const [selectImage, setSelectedImage] = useState({});
  const [tempImage, setTempImage] = useState({});
  const [isPicked, setIsPicked] = useState({});
  const [isPopUp, setPopUp] = useState(false);

  const onFileUpload = async (e) => {
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = () => {
      setTempImage({ ...tempImage, [e.target.id]: reader.result });
    };
    setIsPicked(true);
    setSelectedImage({ ...selectImage, [e.target.id]: e.target.files[0] });
    console.log(e.target.files);
  };

  const quizPostFormatter = (quiz) => {
    const postquizValues = {
      end_time: formatISO(quiz.end_time, { representation: "time" }),
      start_time: formatISO(quiz.start_time, { representation: "time" }),
      date: formatISO(quiz.quiz_date, { representation: "date" }),
      title: quiz.quiz_title,
      description: quiz.quiz_description,
      is_randomized: quiz.isRandomized,
      display_individual: false,
      group: [quiz.whoseQuizInfo.group],
      instructor: [user.id],
      course_id: quiz.whoseQuizInfo.course,
    };

    return postquizValues;
  };

  const quizQuestionPostFormatter = (question, index, newQuizId) => {
    question.answer = [question.answer];
    question.question_image = null;
    if (question.options && question.options.length) {
      let newOption = [];
      question.options.map((option) => {
        let formattedOption = {
          image: "",
          text: option,
        };
        newOption.push(formattedOption);
      });

      question.options = JSON.stringify(newOption);
    }
    question.quiz_id = newQuizId;
    return question;
  };

  const onSubmitHandler = async (values) => {
    let quiz = values;
    let questions = quiz.questions;
    delete quiz.questions;

    quiz = quizPostFormatter(quiz);

    let newQuizId = null;

    let postResponse = await callAPI({
      endpoint: `/api/v1/quiz/`,
      method: "POST",
      data: quiz,
    });
    newQuizId = postResponse.data.id;

    if (postResponse.status === 200 && newQuizId) {
      console.log(newQuizId);
      if (questions) {
        questions.map(async (question, index) => {
          let postQuestion = quizQuestionPostFormatter(
            question,
            index,
            newQuizId
          );
          if (question) {
            postResponse = await callAPI({
              endpoint: `/api/v1/quiz/${newQuizId}/question`,
              method: "POST",
              data: postQuestion,
            });

            let newquestionId = postResponse.data.id;
            let questionImageData = new FormData();
            if (postResponse.status === 200 && selectImage[`${index}`]) {
              questionImageData.append("files", selectImage[`${index}`]);

              let imageResponse = await callAPI({
                endpoint: `/api/v1/quiz/${newQuizId}/question/${newquestionId}/question_image/`,
                method: "POST",
                data: questionImageData,
                headers: { "Content-Type": "multipart/form-data" },
              });

              console.log(imageResponse);
            }
          }
        });
      }
    }
    setSelectedImage({});
  };

  return (
    <DashboardLayout>
      <Grid
        container
        direction="column"
        justify="center"
        alignItems="center"
        className="quizCreator_root"
      >
        <Grid item className="quizCreator_header">
          <a className="quizCreator_titleText">Quiz Creation Menu</a>
        </Grid>
        <Grid item className="quizCreator_body">
          <Grid item className="quizCreator_outerContainer">
            <Formik
              enableReinitialize={true}
              initialValues={{
                quiz_title: "",
                quiz_description: "",
                quiz_date: new Date(),
                start_time: new Date(),
                end_time: new Date(),
                isRandomized: false,
                whoseQuizInfo: null,
              }}
              validationSchema={validationSchema}
              onSubmit={(values) => {
                onSubmitHandler(values);
              }}
            >
              {({ values, setFieldValue }) => (
                <>
                  <Form className="quizCreator_formBox">
                    <Grid
                      container
                      direction="column"
                      alignItems="center"
                      justify="center"
                      className="quizCreator_innerContainer"
                      spacing={3}
                    >
                      <Grid
                        item
                        xs={12}
                        className="quizCreator_titleFieldContainer"
                      >
                        <CustomTextField
                          id="quiz_title"
                          name="quiz_title"
                          placeholder="Enter the title of the quiz"
                          className="quizCreator_titleField"
                        />
                      </Grid>
                      <Grid
                        item
                        className="quizCreator_descriptionFieldContainer"
                      >
                        <CustomTextField
                          id="quiz_description"
                          name="quiz_description"
                          placeholder="Description of the quiz"
                          className="quizCreator_descriptionField"
                        />
                      </Grid>
                      <Grid item className="quizCreator_groupBoxOuter">
                        <CustomTextField
                          name="whoseQuizInfo"
                          dropdown={true}
                          menuItems={groupList}
                          addStyles="quizCreator_groupBox"
                          placeHolder="Choose Group"
                        />
                      </Grid>

                      <Grid
                        container
                        direction="row"
                        alignItems="center"
                        justify="center"
                        className="quizCreator_dateTimePickerContainer"
                        spacing={3}
                      >
                        <Grid item className="quizCreator_quizDateField">
                          <DatePicker id="quiz_date" label="Choose quiz date" />
                        </Grid>
                        <Grid item className="quizCreator_quizStartTime">
                          <TimePicker id="start_time" label="Start Time" />
                        </Grid>
                        <Grid item className="quizCreator_quizEndTime">
                          <TimePicker id="end_time" label="End Time" />
                        </Grid>
                      </Grid>
                      <Grid
                        container
                        direction="row"
                        alignItems="center"
                        justify="center"
                        className="quizCreator_randomContainer"
                        wrap="nowrap"
                      >
                        <Grid item className="quizCreator_check">
                          <Checkbox
                            id="is_randomized"
                            name="isRandomized"
                            label="Randomize Questions"
                            className="quizCreator_randomCheckBox"
                          />
                        </Grid>
                      </Grid>

                      <Grid item className="submission">
                        <Grid
                          container
                          className="quizCreator_addQuestion"
                          alignItems="center"
                          justify="center"
                        >
                          <Field name="questions">
                            {() => (
                              <>
                                <FieldArray name="questions">
                                  {(questionHelper) => (
                                    <>
                                      {values.questions &&
                                        values.questions.length !== 0 &&
                                        values.questions.map(
                                          (question, index) => (
                                            <>
                                              <Grid
                                                container
                                                direction="column"
                                                wrap="nowrap"
                                                className="quizCreator_questionRemovecontainer"
                                              >
                                                <div key={index + 1}>
                                                  <Grid
                                                    container
                                                    directon="row"
                                                    justify="center"
                                                    alignItems="center"
                                                    wrap="nowrap"
                                                    className="quizCreator_questionTitleContainer"
                                                  >
                                                    <Grid item xs={12}>
                                                      <h4 className="quizCreator_questionNumber">
                                                        Question #{index + 1}
                                                      </h4>
                                                    </Grid>
                                                    <Grid
                                                      item
                                                      xs={1}
                                                      className="quizCreator_imageContainerOuter"
                                                    >
                                                      {isPicked ? (
                                                        <Grid
                                                          container
                                                          direction="row"
                                                          justify="center"
                                                          alignItems="center"
                                                          wrap="nowrap"
                                                        >
                                                          <Grid item>
                                                            <Image
                                                              src={tempImage}
                                                              addStyles="quizCreator_uploadedImage"
                                                              onCLick={() => {
                                                                setPopUp(true);
                                                              }}
                                                            />
                                                          </Grid>
                                                          <Grid item>
                                                            <AiOutlineFileImage
                                                              size={30}
                                                              color={
                                                                colorscheme.purple2
                                                              }
                                                              className="quizCreator_fileUploadedIcon"
                                                            />
                                                          </Grid>
                                                        </Grid>
                                                      ) : (
                                                        <label
                                                          for={index}
                                                          className="quizCreator_imageContainer"
                                                        >
                                                          <BsCloudUpload
                                                            color={
                                                              colorscheme.purple2
                                                            }
                                                            size={23}
                                                            className="quizCreator_uploadButton"
                                                            style={{
                                                              float: "right",
                                                              cursor: "pointer",
                                                            }}
                                                          />

                                                          <input
                                                            id={index}
                                                            type="file"
                                                            accept="image/*"
                                                            multiple={true}
                                                            onChange={(e) => {
                                                              onFileUpload(
                                                                e,
                                                                index
                                                              );
                                                            }}
                                                            style={{
                                                              display: "none",
                                                            }}
                                                          ></input>
                                                        </label>
                                                      )}
                                                    </Grid>

                                                    <Grid
                                                      item
                                                      xs={1}
                                                      className="quizCreator_removeContainer"
                                                    >
                                                      <button
                                                        type="button"
                                                        title="Remove Question"
                                                        className="quizCreator_remove"
                                                        onClick={() => {
                                                          setIsPicked(false);
                                                          setSelectedImage({});
                                                          setTempImage({});
                                                          questionHelper.remove(
                                                            index
                                                          );
                                                          answerList.splice(
                                                            index,
                                                            1
                                                          );
                                                        }}
                                                      >
                                                        <ImCross
                                                          size={20}
                                                          color={
                                                            colorscheme.red2
                                                          }
                                                        />
                                                      </button>
                                                    </Grid>
                                                  </Grid>
                                                  <Grid
                                                    item
                                                    xs={12}
                                                    className="quizCreator_questionTitleOuter"
                                                  >
                                                    <CustomTextField
                                                      name={`questions[${index}].question_text`}
                                                      addStyles="quizCreator_questionTitle"
                                                      type="text"
                                                      placeHolder="Question Title"
                                                    />
                                                  </Grid>

                                                  {/* <Grid item xs={12}>
                                                    <CustomTextField
                                                      addStyles="quizCreator_dropdown"
                                                      dropdown={true}
                                                      name={`questions[${index}].question_type`}
                                                      menuItems={questionType}
                                                      placeHolder="Question Type"
                                                    />
                                                  </Grid> */}
                                                </div>
                                              </Grid>
                                              <Grid
                                                container
                                                direction="column"
                                                alignItems="center"
                                                justify="center"
                                              >
                                                <FieldArray
                                                  name={`questions[${index}].options`}
                                                >
                                                  {(newHelper) => (
                                                    <>
                                                      <Grid
                                                        container
                                                        direction="row"
                                                        alignItems="center"
                                                        justify="center"
                                                      >
                                                        <Grid item>
                                                          <button
                                                            type="button"
                                                            className="quizCreator_addOptions"
                                                            style={
                                                              isPicked
                                                                ? {
                                                                    // display:
                                                                    // 	"none",
                                                                  }
                                                                : {}
                                                            }
                                                            onClick={() => {
                                                              newHelper.push();
                                                              answerList[
                                                                index
                                                              ].push({
                                                                name: `Option ${
                                                                  question
                                                                    .options
                                                                    .length + 1
                                                                }`,
                                                                value:
                                                                  question
                                                                    .options
                                                                    .length + 1,
                                                              });
                                                            }}
                                                          >
                                                            Add Options
                                                          </button>
                                                        </Grid>
                                                        <Grid item>
                                                          <a
                                                            className="quizCreator_or"
                                                            style={
                                                              isPicked
                                                                ? {
                                                                    // display:
                                                                    // 	"none",
                                                                  }
                                                                : {}
                                                            }
                                                          >
                                                            OR
                                                          </a>
                                                        </Grid>
                                                        <Grid
                                                          item
                                                          xs={2}
                                                          className="quizCreator_imageContainerOuter1"
                                                        >
                                                          <label
                                                            for={index}
                                                            className="quizCreator_imageContainer"
                                                          >
                                                            <a className="quizCreator_fileUploadtext">
                                                              {!isPicked
                                                                ? "File Upload"
                                                                : "filename.jpg"}
                                                            </a>

                                                            <BsCloudUpload
                                                              color={
                                                                colorscheme.purple2
                                                              }
                                                              size={23}
                                                              className="quizCreator_uploadButton"
                                                              style={{
                                                                position:
                                                                  "relative",
                                                                top: "6px",
                                                                cursor:
                                                                  "pointer",
                                                              }}
                                                            />

                                                            <input
                                                              id={index}
                                                              type="file"
                                                              accept="image/*"
                                                              onChange={(e) => {
                                                                onFileUpload(
                                                                  e,
                                                                  index
                                                                );
                                                              }}
                                                              style={{
                                                                display: "none",
                                                              }}
                                                            ></input>
                                                          </label>
                                                        </Grid>
                                                      </Grid>

                                                      {question.options &&
                                                        question.options
                                                          .length !== 0 &&
                                                        question.options.map(
                                                          (
                                                            option,
                                                            optionIndex
                                                          ) => (
                                                            <div
                                                              key={optionIndex}
                                                            >
                                                              <Grid container>
                                                                <Grid
                                                                  item
                                                                  xs={12}
                                                                >
                                                                  <CustomTextField
                                                                    addStyles="quizCreator_option"
                                                                    name={`questions[${index}].options[${optionIndex}]`}
                                                                    placeHolder={`Option ${
                                                                      optionIndex +
                                                                      1
                                                                    }`}
                                                                  />
                                                                </Grid>
                                                                <Grid
                                                                  item
                                                                  xs={2}
                                                                  className="quizCreator_imageContainerOuter1"
                                                                >
                                                                  <label
                                                                    for={index}
                                                                    className="quizCreator_imageContainer"
                                                                  >
                                                                    <a className="quizCreator_fileUploadtext">
                                                                      {!isPicked
                                                                        ? "File Upload"
                                                                        : "filename.jpg"}
                                                                    </a>

                                                                    <BsCloudUpload
                                                                      color={
                                                                        colorscheme.purple2
                                                                      }
                                                                      size={23}
                                                                      className="quizCreator_uploadButton"
                                                                      style={{
                                                                        position:
                                                                          "relative",
                                                                        top: "6px",
                                                                        cursor:
                                                                          "pointer",
                                                                      }}
                                                                    />

                                                                    <input
                                                                      id={index}
                                                                      type="file"
                                                                      accept="image/*"
                                                                      onChange={(
                                                                        e
                                                                      ) => {
                                                                        onFileUpload(
                                                                          e,
                                                                          index
                                                                        );
                                                                      }}
                                                                      style={{
                                                                        display:
                                                                          "none",
                                                                      }}
                                                                    ></input>
                                                                  </label>
                                                                </Grid>
                                                              </Grid>
                                                            </div>
                                                          )
                                                        )}
                                                      <Grid
                                                        item
                                                        className="quizCreator_final"
                                                        xs={12}
                                                      >
                                                        <CustomTextField
                                                          addStyles="quizCreator_correct"
                                                          dropdown={true}
                                                          name={`questions[${index}].answer`}
                                                          menuItems={
                                                            answerList[index] ||
                                                            []
                                                          }
                                                          placeHolder="Choose correct Option"
                                                        />
                                                      </Grid>
                                                    </>
                                                  )}
                                                </FieldArray>
                                              </Grid>
                                            </>
                                          )
                                        )}
                                      <Grid
                                        item
                                        className="quizCreator_addQuestionButtonContainer"
                                      >
                                        <button
                                          type="button"
                                          className="quizCreator_addQuestionButton"
                                          onClick={() => {
                                            questionHelper.push(
                                              questionInitialValue
                                            );
                                            answerList.push([]);
                                          }}
                                        >
                                          Add Question
                                        </button>
                                      </Grid>
                                    </>
                                  )}
                                </FieldArray>
                              </>
                            )}
                          </Field>
                        </Grid>
                        <Grid
                          container
                          alignItems="center"
                          justify="center"
                          direction="row"
                        >
                          <Grid
                            item
                            className="quizCreator_submitButtonContainer"
                          >
                            <button
                              type="submit"
                              className="quizCreator_submitButton"
                            >
                              Submit
                            </button>
                          </Grid>
                        </Grid>
                      </Grid>
                    </Grid>
                  </Form>
                </>
              )}
            </Formik>
          </Grid>
        </Grid>
      </Grid>

      <Grid
        container
        direction="row"
        alignItems="flex-start"
        justify="center"
        className="quizCreator_popup"
        style={
          !isPopUp
            ? {
                display: "none",
              }
            : {}
        }
        spacing={6}
      >
        <Grid item xs={11} className="quizCreator_imageContainer">
          <Image src={tempImage} addStyles="quizCreator_imageContainer" />
        </Grid>
        <Grid item>
          <ImCross
            color={colorscheme.green4}
            className="quizCreator_closeButton"
            onClick={() => {
              setPopUp(false);
            }}
          />
        </Grid>
      </Grid>
    </DashboardLayout>
  );
};

export default QuizCreator;
