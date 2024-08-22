import { ISessionContext } from '@jupyterlab/apputils';
import { CodeCell } from '@jupyterlab/cells';
import { OutputArea } from '@jupyterlab/outputarea';
import { Kernel, KernelMessage } from '@jupyterlab/services';
import { JSONObject } from '@lumino/coreutils';

/**
 * Execute a cell given a client session.
 */
export async function execute(
  cell: CodeCell,
  sessionContext: ISessionContext,
  metadata?: JSONObject
): Promise<KernelMessage.IExecuteReplyMsg | void> {
  const model = cell.model;
  const isVisualCode = model.getMetadata('code type') === 'visual code';
  let code = '';
  const currentKernel: any = sessionContext.session?.kernel;
  currentKernel?.registerCommTarget('capture_image', (comm: any, msg: any) => {
    comm.onMsg = (msg: any) => {
      // Base64-encoded image data
      const imageDomId: string = msg.content.data.image_dom_id;
      const imageData = msg.content.data.image_data;
      const imageElement = document.getElementById(
        imageDomId
      ) as HTMLImageElement;
      if (imageElement) {
        imageElement.src = `data:image/png;base64,${imageData}`;
      } else {
        console.error(
          `image element ${imageDomId} not found, cannot set display intermediate image`
        );
      }
    };
  });

  if (isVisualCode && cell.editor) {
    const result = (cell.editor as any).editor.getCode();
    if (result.hasError) {
      cell.outputArea.model.clear();
      cell.outputArea.model.add({
        output_type: 'error',
        ename: 'Error',
        evalue: result.result,
        traceback: []
      });
      return;
    } else {
      code = result.code;
    }
  } else {
    code = model.sharedModel.getSource();
  }

  if (!code.trim() || !sessionContext.session?.kernel) {
    model.sharedModel.transact(() => {
      model.clearExecution();
    }, false);
    return;
  }
  const cellId = { cellId: model.sharedModel.getId() };
  metadata = {
    ...model.metadata,
    ...metadata,
    ...cellId
  };
  const { recordTiming } = metadata;
  model.sharedModel.transact(() => {
    model.clearExecution();
    cell.outputHidden = false;
  }, false);
  cell.setPrompt('*');
  model.trusted = true;
  let future:
    | Kernel.IFuture<
        KernelMessage.IExecuteRequestMsg,
        KernelMessage.IExecuteReplyMsg
      >
    | undefined;
  try {
    const msgPromise = OutputArea.execute(
      code,
      cell.outputArea,
      sessionContext,
      metadata
    );
    // cell.outputArea.future assigned synchronously in `execute`
    if (recordTiming) {
      const recordTimingHook = (msg: KernelMessage.IIOPubMessage) => {
        let label: string;
        switch (msg.header.msg_type) {
          case 'status':
            label = `status.${
              (msg as KernelMessage.IStatusMsg).content.execution_state
            }`;
            break;
          case 'execute_input':
            label = 'execute_input';
            break;
          default:
            return true;
        }
        // If the data is missing, estimate it to now
        // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header
        const value = msg.header.date || new Date().toISOString();
        const timingInfo: any = Object.assign(
          {},
          model.getMetadata('execution')
        );
        timingInfo[`iopub.${label}`] = value;
        model.setMetadata('execution', timingInfo);
        return true;
      };
      cell.outputArea.future.registerMessageHook(recordTimingHook);
    } else {
      model.deleteMetadata('execution');
    }
    // Save this execution's future so we can compare in the catch below.
    future = cell.outputArea.future;
    const msg = (await msgPromise)!;
    model.executionCount = msg.content.execution_count;
    if (recordTiming) {
      const timingInfo = Object.assign(
        {},
        model.getMetadata('execution') as any
      );
      const started = msg.metadata.started as string;
      // Started is not in the API, but metadata IPyKernel sends
      if (started) {
        timingInfo['shell.execute_reply.started'] = started;
      }
      // Per above, the 5.0 spec does not assume date, so we estimate is required
      const finished = msg.header.date as string;
      timingInfo['shell.execute_reply'] = finished || new Date().toISOString();
      model.setMetadata('execution', timingInfo);
    }
    return msg;
  } catch (e) {
    // If we started executing, and the cell is still indicating this
    // execution, clear the prompt.
    if (future && !cell.isDisposed && cell.outputArea.future === future) {
      cell.setPrompt('');
    }
    throw e;
  }
}

export function enhanceCodeCellExecute() {
  // monkey patch the execute method of CodeCell
  CodeCell.execute = execute;
}
